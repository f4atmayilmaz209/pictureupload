"use client"

import { useState } from "react";


export default function Home() {

  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!file) {
      setMessage("Lütfen bir dosya seçin.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setMessage("Yükleme başarılı! PNG dosyası döndü.");
        console.log("Server response:", data);
      } else {
        setMessage("Yükleme başarısız.");
      }
    } catch (error) {
      console.error("Upload error:", error);
      setMessage("Sunucu hatası.");
    }
  };


  return (
    <div className="p-6 flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Upload Image</h1>
      <form onSubmit={handleSubmit} className="space-y-4 flex flex-col ml-20">
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded w-[140px]">
          Upload Image
        </button>
      </form>
      {message && <p className="mt-4 text-lg">{message}</p>}
    </div>
  );
}
