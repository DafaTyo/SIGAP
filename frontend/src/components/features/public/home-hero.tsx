"use client";

import Image from "next/image";
import Link from "next/link";
import { motion } from "motion/react";

export function HomeHero() {
  return (
    <section className="bg-gray-50 py-12 sm:py-16">
      <div className="mx-auto flex max-w-7xl flex-col items-center gap-10 px-4 sm:px-6 lg:flex-row lg:gap-16 lg:px-16">
        {/* Left Text */}
        <motion.div
          initial={{ opacity: 0, x: -24 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className="max-w-lg shrink-0 text-center lg:text-left transition-all duration-300"
        >
          <h1 className="font-bold leading-tight text-[#2563EB]" style={{ fontSize: "var(--text-fluid-4xl)" }}>
            Pantau Makanan Sehat di Wilayah Kamu
          </h1>
          <p className="mt-4 leading-relaxed text-gray-500" style={{ fontSize: "var(--text-fluid-base)" }}>
            Pantau perizinan vendor, sebaran dapur, dan keamanan pangan di sekitar lingkunganmu.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4 lg:justify-start">
            <Link
              href="/public/vendors/search"
              className="inline-flex items-center gap-2 rounded-lg bg-[#2563EB] px-5 py-3 text-sm font-semibold text-white hover:bg-[#2563EB]/90 transition-colors"
            >
              <svg width="16" height="16" viewBox="0 0 21 21" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7.68006 5.58184V17.7461M12.8001 2.71464V14.8789M2.56006 7.33288C2.56006 6.02984 2.56006 5.37875 2.89542 4.99902C3.01403 4.86334 3.15825 4.75582 3.31953 4.68158C4.52785 4.12435 6.11163 5.59123 7.38993 5.546C7.55889 5.53975 7.72585 5.51642 7.89083 5.47603C9.75451 5.0195 10.9219 2.84776 12.8385 2.58323C13.9367 2.42963 15.1425 3.09352 16.1699 3.44851C17.0147 3.74035 17.4371 3.88627 17.6786 4.23358C17.9201 4.58088 17.9201 5.04339 17.9201 5.96499V13.1518C17.9201 14.454 17.9201 15.1059 17.5847 15.4856C17.4669 15.6196 17.3225 15.7274 17.1606 15.8022C15.9523 16.3594 14.3685 14.8934 13.0902 14.9386C12.9214 14.9451 12.7536 14.9683 12.5893 15.0078C10.7256 15.4643 9.55825 17.636 7.64166 17.9014C6.54854 18.0533 3.50555 17.2614 2.80155 16.2502C2.56006 15.9029 2.56006 15.4421 2.56006 14.5188V7.33288Z" stroke="currentColor" strokeWidth="0.96" strokeLinecap="round" strokeLinejoin="round"/>
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
