"use client";

import Image from "next/image";
import Link from "next/link";
import { motion } from "motion/react";

export function HomeHero() {
  return (
    <section className="bg-gray-50 py-16">
      <div className="mx-auto flex max-w-7xl items-center gap-16 px-4 sm:px-6 lg:px-16">
        {/* Left Text */}
        <motion.div
          initial={{ opacity: 0, x: -24 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="max-w-lg shrink-0"
        >
          <h1 className="text-4xl font-bold leading-tight text-[#2563EB] sm:text-5xl">
            Pantau Makanan Sehat di Wilayah Kamu
          </h1>
          <p className="mt-4 text-base leading-relaxed text-gray-500">
            Pantau perizinan vendor, sebaran dapur, dan keamanan pangan di sekitar lingkunganmu.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              href="/public/vendors/search"
              className="inline-flex items-center gap-2 rounded-lg bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white hover:bg-[#2563EB]/90 transition-colors"
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 1.5C5.5 1.5 3.5 3.5 3.5 6C3.5 9.5 8 14.5 8 14.5C8 14.5 12.5 9.5 12.5 6C12.5 3.5 10.5 1.5 8 1.5Z" fill="currentColor"/>
                <circle cx="8" cy="6" r="1.5" fill="white"/>
              </svg>
              Pantau Wilayah SPPG Kamu
            </Link>
            <Link
              href="/public/vendors/register"
              className="inline-flex items-center gap-2 rounded-lg border border-[#0D9488] px-5 py-3 text-sm font-semibold text-[#0D9488] hover:bg-teal-50 transition-colors"
            >
              Daftar menjadi Mitra SPPG
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 8H13M13 8L9.5 4.5M13 8L9.5 11.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </Link>
          </div>
        </motion.div>

        {/* Right Illustration */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2, ease: "easeOut" }}
          className="hidden flex-1 lg:block"
        >
          <Image
            src="/assets/images/dashboard_banner.png"
            alt="Ilustrasi cakupan layanan SIGAP"
            width={1260}
            height={840}
            className="h-auto w-full object-contain"
            priority
          />
        </motion.div>
      </div>
    </section>
  );
}
