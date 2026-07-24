"use client";

import { motion, type Variants } from "motion/react";

export function HowItWorks() {
  const container: Variants = {
    hidden: {},
    visible: { transition: { staggerChildren: 0.1 } },
  };

  const item: Variants = {
    hidden: { opacity: 0, y: 24 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" as const } },
  };

  const cards = [
    {
      title: "Vendor Terdaftar",
      desc: "Terverifikasi NIB & Dokumen",
      bg: "bg-blue-50",
      iconBg: "bg-blue-100",
      iconColor: "text-[#2563EB]",
      svg: (
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="4" y="8" width="24" height="20" rx="2" stroke="currentColor" strokeWidth="1.5"/>
          <path d="M10 4H22V8H10V4Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
          <path d="M12 18L15 21L20 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
    },
    {
      title: "Monitoring Real Time",
      desc: "Pantau Kuota & Jangkauan",
      bg: "bg-teal-50",
      iconBg: "bg-teal-100",
      iconColor: "text-teal-600",
      svg: (
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="4" y="6" width="24" height="20" rx="2" stroke="currentColor" strokeWidth="1.5"/>
          <path d="M12 22V14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <path d="M16 22V10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <path d="M20 22V16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          <path d="M4 26H28" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
      ),
    },
    {
      title: "Laporan Transparan",
      desc: "Masyarakat Melapor & Mengecek",
      bg: "bg-yellow-50",
      iconBg: "bg-yellow-100",
      iconColor: "text-yellow-600",
      svg: (
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M16 4C9.5 4 5 8.5 5 12C5 15 7 17.5 10 19L9 28L16 23L23 28L22 19C25 17.5 27 15 27 12C27 8.5 22.5 4 16 4Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/>
        </svg>
      ),
    },
    {
      title: "Sertifikasi Digital",
      desc: "Terbit SIO & Verifikasi Instan",
      bg: "bg-gray-50",
      iconBg: "bg-gray-100",
      iconColor: "text-gray-600",
      svg: (
        <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="16" cy="16" r="12" stroke="currentColor" strokeWidth="1.5"/>
          <path d="M12 16L15 19L20 13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      ),
    },
  ];

  return (
    <section className="bg-gray-50 py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-16 text-center">
        <motion.h2
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3 }}
          className="text-3xl font-bold text-[#2563EB]"
        >
          Bagaimana SIGAP Bekerja
        </motion.h2>
        <motion.div
          variants={container}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4"
        >
          {cards.map((card) => (
            <motion.div
              key={card.title}
              variants={item}
              whileHover={{ y: -6, transition: { duration: 0.2 } }}
              className={`flex flex-col items-center rounded-2xl border border-gray-100 ${card.bg} px-8 py-10 shadow-sm`}
            >
              <div className={`flex h-14 w-14 items-center justify-center rounded-xl ${card.iconBg} ${card.iconColor}`}>
                {card.svg}
              </div>
              <h3 className="mt-5 text-base font-semibold text-[#2563EB]">{card.title}</h3>
              <p className="mt-1.5 text-sm text-gray-400">{card.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
