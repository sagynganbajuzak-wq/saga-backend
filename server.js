const express = require('express');
const multer  = require('multer');
const path = require('path');
const app = express();

// Настраиваем папку, куда будут падать фото и аудио
const storage = multer.diskStorage({
    destination: './uploads/',
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname));
    }
});
const upload = multer({ storage: storage });

// Делаем папку uploads доступной по ссылке в интернете
app.use('/uploads', express.static('uploads'));

// Тот самый endpoint /upload, который ищет твой Android
app.post('/upload', upload.single('file'), (req, res) => {
    if (!req.file) return res.status(400).send('Файл не получен');

    // Возвращаем приложению прямую ссылку на файл на твоем жестком диске
    const fileUrl = `${req.protocol}://${req.get('host')}/uploads/${req.file.filename}`;
    res.send(fileUrl);
});

app.listen(3000, () => console.log('Сервер запущен на порту 3000!'));