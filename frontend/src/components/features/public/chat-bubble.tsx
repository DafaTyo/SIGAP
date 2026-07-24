"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { X, Minus, Send, Bot, User } from "lucide-react";

const faqReplies: Record<string, string> = {
  "halo": "Halo! Ada yang bisa kami bantu? Silakan tanya seputar vendor, pengaduan, atau informasi SIGAP lainnya.",
  "vendor": "Untuk mendaftar sebagai mitra SPPG, silakan kunjungi halaman Daftar Mitra. Pastikan Anda memiliki NIB dan dokumen pendukung lainnya.",
  "pengaduan": "Untuk melaporkan pengaduan, silakan gunakan menu Layanan Pengaduan. Kami akan memproses laporan Anda dalam 1x24 jam.",
  "default": "Maaf, saya belum bisa menjawab pertanyaan itu. Silakan hubungi tim support kami melalui menu Layanan Pengaduan atau coba tanyakan hal lain.",
};

function getReply(input: string): string {
  const lower = input.toLowerCase();
  if (lower.includes("halo") || lower.includes("hai") || lower.includes("hi")) return faqReplies["halo"];
  if (lower.includes("vendor") || lower.includes("mitra") || lower.includes("daftar")) return faqReplies["vendor"];
  if (lower.includes("pengaduan") || lower.includes("lapor") || lower.includes("komplain")) return faqReplies["pengaduan"];
  return faqReplies["default"];
}

export function ChatBubble() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<{ role: "bot" | "user"; text: string }[]>([
    { role: "bot", text: "Halo! Ada yang bisa kami bantu?" },
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    const userMsg = input.trim();
    setMessages((prev) => [...prev, { role: "user", text: userMsg }]);
    setInput("");
    setTimeout(() => {
      setMessages((prev) => [...prev, { role: "bot", text: getReply(userMsg) }]);
    }, 600);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <>
      {/* Trigger Button */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            onClick={() => setIsOpen(true)}
            className="fixed bottom-4 right-4 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-[#0D9488] text-white shadow-lg hover:bg-[#0D9488]/90 transition-colors sm:bottom-6 sm:right-6"
          >
            <Bot className="h-6 w-6" />
          </motion.button>
        )}
      </AnimatePresence>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 32, scale: 0.95 }}
            animate={isMinimized ? { opacity: 0, y: 32, scale: 0.95 } : { opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 32, scale: 0.95 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="fixed bottom-4 right-4 z-50 flex w-[calc(100vw-32px)] flex-col overflow-hidden rounded-2xl bg-white shadow-2xl sm:bottom-6 sm:right-6 sm:w-[360px]"
            style={{ height: isMinimized ? 0 : 520 }}
          >
            {/* Header */}
            <div className="flex items-center justify-between bg-[#0D9488] px-4 py-3">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-white/20">
                  <Bot className="h-5 w-5 text-white" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-white">SIGAP Asisten AI</p>
                  <div className="flex items-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-green-400" />
                    <span className="text-xs text-white/80">Siap Membantu</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setIsMinimized(!isMinimized)}
                  className="flex h-7 w-7 items-center justify-center rounded-md text-white/80 hover:bg-white/20 transition-colors"
                >
                  <Minus className="h-4 w-4" />
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="flex h-7 w-7 items-center justify-center rounded-md text-white/80 hover:bg-white/20 transition-colors"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 space-y-4 overflow-y-auto px-4 py-4">
              {messages.map((msg, i) => (
                <div key={i} className={`flex items-start gap-2.5 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                  <div
                    className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
                      msg.role === "bot" ? "bg-[#0D9488]" : "bg-[#0D9488]"
                    }`}
                  >
                    {msg.role === "bot" ? (
                      <Bot className="h-4 w-4 text-white" />
                    ) : (
                      <User className="h-4 w-4 text-white" />
                    )}
                  </div>
                  <div
                    className={`max-w-[70vw] rounded-2xl px-4 py-2.5 text-sm leading-relaxed sm:max-w-[260px] ${
                      msg.role === "bot"
                        ? "rounded-bl-sm border border-gray-100 bg-white text-gray-700"
                        : "rounded-br-sm bg-teal-50 text-gray-700"
                    }`}
                  >
                    {msg.text}
                  </div>
                </div>
              ))}
            </div>

            {/* Input */}
            <div className="border-t border-gray-100 px-4 py-3">
              <div className="flex items-center gap-2">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ketik pertanyaan Anda..."
                  className="flex-1 rounded-xl border border-gray-200 px-4 py-2.5 text-sm outline-none placeholder:text-gray-400 focus:border-teal-500"
                />
                <button
                  onClick={handleSend}
                  className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#0D9488] text-white hover:bg-[#0D9488]/90 transition-colors"
                >
                  <Send className="h-4 w-4" />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}