CREATE OR REPLACE FUNCTION hitung_kartu_merah()
RETURNS TRIGGER AS $$
DECLARE
    jumlah_kartu_merah INTEGER;
    jumlah_kartu_kuning INTEGER;
BEGIN
    SELECT COUNT(*) INTO jumlah_kartu_merah
    FROM peristiwa
    WHERE id_pemain = NEW.id_pemain
    AND jenis = 'Kartu Merah'
    AND datetime = NEW.datetime;
    SELECT COUNT(*) INTO jumlah_kartu_kuning
    FROM peristiwa
    WHERE id_pemain = NEW.id_pemain
    AND jenis = 'Kartu Kuning'
    AND datetime = NEW.datetime;
    IF jumlah_kartu_merah > 0 THEN
        RAISE EXCEPTION 'Pemain sudah terkena kartu merah';
    END IF;
    RETURN NEW;
    IF jumlah_kartu_kuning = 2 THEN
        INSERT INTO peristiwa
        VALUES (id_pertandingan, NEW.datetime, jenis, NEW.id_pemain);
    END IF;
    RETURN NEW;
END;
LANGUAGE plpgsql;

CREATE TRIGGER kartu_merah
BEFORE INSERT ON peristiwa
FOR EACH ROW
EXECUTE PROCEDURE hitung_kartu_merah();



