"use client";

import Image from "next/image";
import { motion } from "motion/react";

export function AboutVision() {
  return (
    <section className="bg-white py-12 sm:py-16">
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

        <div className="mt-8 grid items-center gap-8 lg:mt-10 lg:grid-cols-2 lg:gap-12">
          {/* Left Text */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          >
            <h2 className="font-bold text-[#2563EB]" style={{ fontSize: "var(--text-fluid-3xl)" }}>VISI KAMI</h2>
            <p className="mt-4 leading-relaxed text-gray-500" style={{ fontSize: "var(--text-fluid-base)" }}>
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
              className="h-auto w-full max-w-[320px] object-contain sm:max-w-[420px]"
            />
          </motion.div>
        </div>
      </div>
    </section>
  );
}
