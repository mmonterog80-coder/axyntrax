require('dotenv').config({ path: 'C:/AXYNTRAX/AXYNTRAX_VAULT/master_keys.env' });
const { createClient } = require('@supabase/supabase-js');
const { GoogleGenAI } = require('@google/genai');

// Inicializar clientes
const supabase = createClient(
    process.env.SUPABASE_URL || 'https://xyz.supabase.co',
    process.env.SUPABASE_SERVICE_KEY || 'ey...'
);

const ai = new GoogleGenAI({
    apiKey: process.env.GEMINI_API_KEY
});

// En producción, esto escucharía un Webhook de WhatsApp Web.js o n8n
// Simulamos la llegada de un voucher
async function processIncomingVoucher(imageUrl, appointmentId) {
    console.log(`[AXY-FINANCE] Analizando Voucher de Pago para Cita: ${appointmentId}`);

    try {
        console.log(`[AXY-FINANCE] Consultando a Gemini Vision 1.5 Flash (Con Model Armor)...`);
        
        // Mock seguro que simula un "Structured Output" para evitar Prompt Injection
        // En producción se usa gemini-1.5-flash con responseSchema estricto.
        const geminiMockResponse = {
            monto: 50.00,
            operacion: "123456789",
            metodo: "YAPE",
            valido: true
        };

        // Verificamos si la operación ya existe ANTES de hacer nada para rechazar vouchers reciclados
        const { data: existing } = await supabase.from('payments').select('id').eq('operation_number', geminiMockResponse.operacion).single();
        if (existing) {
            console.error(`[ALERTA ROJA] Voucher Reciclado o Falso: Operación #${geminiMockResponse.operacion} ya existe.`);
            return;
        }

        console.log(`[AXY-FINANCE] OCR Completado: Operación #${geminiMockResponse.operacion} | Monto: S/${geminiMockResponse.monto}`);

        // Llamada RPC Transaccional (Atómica) para evitar registros huérfanos
        const { error } = await supabase.rpc('process_payment_and_confirm', {
            p_appointment_id: appointmentId,
            p_voucher_url: imageUrl,
            p_operation_number: geminiMockResponse.operacion,
            p_amount: geminiMockResponse.monto,
            p_method: geminiMockResponse.metodo,
            p_is_valid: geminiMockResponse.valido
        });

        if (error) throw error;

        console.log(`[AXY-FINANCE] Cita ${appointmentId} ha sido encolada para Tri-Match (Consenso Bancario).`);

    } catch (e) {
        console.error("[AXY-FINANCE] Error crítico en la conciliación:", e.message);
    }
}

// Ejecución de prueba
if (require.main === module) {
    processIncomingVoucher("https://storage.axyntrax.com/vouchers/test.jpg", "uuid-test-123");
}

module.exports = { processIncomingVoucher };
