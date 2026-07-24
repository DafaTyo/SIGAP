"use client";

import Image from "next/image";
import { motion } from "motion/react";

export function AboutVision() {
  return (
    <section className="bg-white py-16">
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
          {/* Left Text */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          >
            <h2 className="text-3xl font-bold text-[#2563EB]">VISI KAMI</h2>
            <p className="mt-4 text-base leading-relaxed text-gray-500">
              Menjadi infrastruktur digital terdepan dalam tata kelola pangan nasional yang transparan, akuntabel, dan presisi, demi menjamin pemenuhan gizi generasi emas Indonesia secara merata.
            </p>
          </motion.div>

          {/* Right Illustration */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.15, ease: "easeOut" }}
            className="flex justify-center"
          >
            <Image
              src="/assets/images/dashboard_about.png"
              alt="Visi SIGAP"
              width={420}
              height={420}
              className="h-auto w-full max-w-[420px] object-contain"
            />
          </motion.div>
        </div>
      </div>
    </section>
  );
}
