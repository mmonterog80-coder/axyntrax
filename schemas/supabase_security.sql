-- ACTIVAR RLS EN TODAS LAS TABLAS
ALTER TABLE supermemory ENABLE ROW LEVEL SECURITY;
ALTER TABLE qwen_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE qwen_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE vet_owners ENABLE ROW LEVEL SECURITY;
ALTER TABLE vet_pets ENABLE ROW LEVEL SECURITY;
ALTER TABLE vet_appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE vet_medical_records ENABLE ROW LEVEL SECURITY;

-- POLÍTICAS RLS BÁSICAS
CREATE POLICY "Allow all for supermemory" ON supermemory FOR ALL USING (true);
CREATE POLICY "Allow all for qwen_orders" ON qwen_orders FOR ALL USING (true);
CREATE POLICY "Allow all for qwen_results" ON qwen_results FOR ALL USING (true);
CREATE POLICY "Allow all for vet tables" ON vet_owners FOR ALL USING (true);
CREATE POLICY "Allow all for vet_pets" ON vet_pets FOR ALL USING (true);
CREATE POLICY "Allow all for vet_appointments" ON vet_appointments FOR ALL USING (true);
CREATE POLICY "Allow all for vet_medical_records" ON vet_medical_records FOR ALL USING (true);

-- LIMPIAR MEMORIA BASURA
DELETE FROM supermemory WHERE length(content) < 20;
DELETE FROM supermemory WHERE content ILIKE '%hola%' OR content ILIKE '%gracias%' OR content ILIKE '%recibí tu mensaje%';
