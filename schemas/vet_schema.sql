-- Schema real para VetManager
CREATE TABLE IF NOT EXISTS vet_owners (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vet_pets (
    id BIGSERIAL PRIMARY KEY,
    owner_id BIGINT REFERENCES vet_owners(id),
    name VARCHAR(100) NOT NULL,
    species VARCHAR(50),
    breed VARCHAR(50),
    birth_date DATE,
    weight_kg DECIMAL(5,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vet_appointments (
    id BIGSERIAL PRIMARY KEY,
    pet_id BIGINT REFERENCES vet_pets(id),
    appointment_date TIMESTAMPTZ NOT NULL,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vet_medical_records (
    id BIGSERIAL PRIMARY KEY,
    pet_id BIGINT REFERENCES vet_pets(id),
    date TIMESTAMPTZ DEFAULT NOW(),
    diagnosis TEXT,
    treatment TEXT,
    prescription TEXT,
    vet_name VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_vet_pets_owner ON vet_pets(owner_id);
CREATE INDEX IF NOT EXISTS idx_vet_appointments_pet ON vet_appointments(pet_id);
CREATE INDEX IF NOT EXISTS idx_vet_appointments_date ON vet_appointments(appointment_date);
