"use client";

import Image from "next/image";
import { motion } from "motion/react";

const missions = [
  {
    number: "01",
    text: "Mempercepat perizinan vendor melalui verifikasi digital end-to-end",
  },
  {
    number: "02",
    text: "Monitoring real-time distribusi pangan hingga ke penerima manfaat",
  },
  {
    number: "03",
    text: "Partisipasi aktif masyarakat melalui kanal pengaduan terstruktur",
  },
  {
    number: "04",
    text: "Menyediakan dashboard analitik untuk pengambilan keputusan strategis",
  },
];

export function AboutMission() {
  return (
    <section className="bg-gray-50 py-16">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-16">
        <motion.p
          initial={{ opacity: 0, y: 8 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3 }}
          className="text-xs font-semibold tracking-[0.2em] text-[#2563EB] uppercase"
        >
          Tentang Kami
        </motion.p>

        <div className="mt-10 grid items-center gap-12 lg:grid-cols-2">
          {/* Left Illustration */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, ease: "easeOut" }}
            className="flex justify-center"
          >
            <Image
              src="/assets/images/dashboard_misi.png"
              alt="Misi SIGAP"
              width={420}
              height={420}
              className="h-auto w-full max-w-[420px] object-contain"
            />
          </motion.div>

          {/* Right Text */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.15, ease: "easeOut" }}
          >
            <h2 className="text-3xl font-bold text-[#2563EB]">MISI KAMI</h2>
            <ul className="mt-6 space-y-5">
              {missions.map((m) => (
                <li key={m.number} className="flex items-start gap-4">
                  <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-blue-100 text-sm font-bold text-[#2563EB]">
                    {m.number}
                  </span>
                  <p className="text-base text-gray-500">{m.text}</p>
                </li>
              ))}
            </ul>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
