"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Menu, X } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";

export function PublicHeader() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-100 bg-white">
      <div className="mx-auto flex h-[72px] max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-16">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2">
          <Image
            src="/assets/images/Logo Dark.png"
            alt="SIGAP"
            width={106}
            height={35}
            className="h-9 w-auto"
            priority
          />
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden items-center gap-6 md:flex">
          <Link href="/" className="text-sm font-medium text-[#2563EB] underline underline-offset-4 decoration-2 decoration-[#2563EB]">
            Beranda
          </Link>
          <Link href="/public/vendors/search" className="text-sm font-medium text-[#64748B] hover:text-[#2563EB] transition-colors">
            Cari Vendor
          </Link>
          <Link href="/public/complaints" className="text-sm font-medium text-[#64748B] hover:text-[#2563EB] transition-colors">
            Layanan Pengaduan
          </Link>
          <Link href="/auth/login" className="rounded-lg bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#2563EB]/90 transition-colors">
            Masuk
          </Link>
        </nav>

        {/* Mobile Hamburger */}
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="flex items-center justify-center rounded-md p-2 text-gray-600 hover:bg-gray-100 md:hidden"
        >
          {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>

      {/* Mobile Nav Overlay */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden border-t border-gray-100 bg-white md:hidden"
          >
            <nav className="flex flex-col gap-4 px-4 pb-6 pt-4 sm:px-6 lg:px-16">
              <Link href="/" onClick={() => setMobileOpen(false)} className="text-sm font-medium text-[#2563EB]">
                Beranda
              </Link>
              <Link href="/public/vendors/search" onClick={() => setMobileOpen(false)} className="text-sm font-medium text-[#64748B]">
                Cari Vendor
              </Link>
              <Link href="/public/complaints" onClick={() => setMobileOpen(false)} className="text-sm font-medium text-[#64748B]">
                Layanan Pengaduan
              </Link>
              <Link
                href="/auth/login"
                onClick={() => setMobileOpen(false)}
                className="inline-flex items-center justify-center rounded-lg bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white"
              >
                Masuk
              </Link>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}