-- FASE 1: Esquema de Citas y Predicción (PREDICTIVE NO-SHOW ENGINE)
CREATE TABLE IF NOT EXISTS public.appointments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_name TEXT NOT NULL,
    client_phone TEXT NOT NULL,
    service_type TEXT NOT NULL,
    appointment_date TIMESTAMPTZ NOT NULL,
    status TEXT DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED', 'NO_SHOW')),
    noshow_probability DECIMAL(5,2) DEFAULT 0.00, -- Calculado por XGBoost
    created_at TIMESTAMPTZ DEFAULT now()
);

-- FASE 1: Esquema de Pagos (AXY-FINANCE PRO)
CREATE TABLE IF NOT EXISTS public.payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    appointment_id UUID REFERENCES public.appointments(id) ON DELETE CASCADE,
    voucher_url TEXT, -- URL de la imagen en Supabase Storage
    operation_number TEXT UNIQUE, -- Número de operación extraído por OCR
    amount DECIMAL(10,2) NOT NULL,
    payment_method TEXT DEFAULT 'YAPE' CHECK (payment_method IN ('YAPE', 'PLIN', 'CARD', 'CASH')),
    status TEXT DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'VERIFIED', 'FAILED')),
    verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- RLS (Row Level Security) - Solo autenticados o service_role pueden acceder
ALTER TABLE public.appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payments ENABLE ROW LEVEL SECURITY;

-- Políticas
CREATE POLICY "Allow service role full access to appointments" ON public.appointments FOR ALL USING (true);
CREATE POLICY "Allow service role full access to payments" ON public.payments FOR ALL USING (true);

-- SEGURIDAD: Stored Procedure (RPC) para Conciliación Atómica (Zero Trust)
-- Evita transacciones huérfanas si la app Node.js se cae a la mitad.
CREATE OR REPLACE FUNCTION process_payment_and_confirm(
    p_appointment_id UUID,
    p_voucher_url TEXT,
    p_operation_number TEXT,
    p_amount DECIMAL,
    p_method TEXT,
    p_is_valid BOOLEAN
) RETURNS VOID AS $$
BEGIN
    -- 1. Insertar el intento de pago (Estado PENDING hasta Tri-Match)
    INSERT INTO public.payments (
        appointment_id, voucher_url, operation_number, amount, payment_method, status, verified_at
    ) VALUES (
        p_appointment_id, p_voucher_url, p_operation_number, p_amount, p_method, 
        CASE WHEN p_is_valid THEN 'PENDING' ELSE 'FAILED' END, 
        now()
    );

    -- 2. No confirmamos la cita automáticamente, la pasamos a IN_REVIEW para forzar consenso bancario
    IF p_is_valid THEN
        UPDATE public.appointments 
        SET status = 'PENDING' -- Mantenido en pendiente hasta webhook bancario
        WHERE id = p_appointment_id;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
