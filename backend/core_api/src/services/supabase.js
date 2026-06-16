const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL || 'https://placeholder.supabase.co';
// JARVIS Instruction: Read the token directly from master_keys.env
const supabaseKey = process.env.SUPABASE_ACCESS_TOKEN; 

if (!supabaseKey) {
    console.warn('[WARNING] SUPABASE_ACCESS_TOKEN no encontrado en master_keys.env');
}

const supabase = createClient(supabaseUrl, supabaseKey);

module.exports = supabase;
