"tampilkan nama depan, nama belakang, nomor hp, email, alamat, status, dan detail tim dari manager dengan id amartusewicz2"
SELECT np.nama_depan, np.nama_belakang, np.nomor_hp, np.email, np.alamat, nps.status, tm.nama_tim
FROM manajer m, non_pemain np, status_non_pemain nps, tim_manajer tm
WHERE m.id_manajer = np.id AND np.id = nps.id_non_pemain AND m.id_manajer = tm.id_manajer AND m.username = 'amartusewicz2';