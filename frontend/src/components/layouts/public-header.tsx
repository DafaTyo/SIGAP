import Image from "next/image";
import Link from "next/link";

export function PublicHeader() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-100 bg-white">
      <div className="mx-auto flex h-[72px] max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-16">
        {/* Logo — Dark variant */}
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

        {/* Navigation */}
        <nav className="flex items-center gap-8">
          <Link
            href="/"
            className="text-sm font-medium text-[#2563EB] underline underline-offset-4 decoration-2 decoration-[#2563EB]"
          >
            Beranda
          </Link>
          <Link
            href="/public/vendors/search"
            className="text-sm font-medium text-[#64748B] hover:text-[#2563EB] transition-colors"
          >
            Cari Vendor
          </Link>
          <Link
            href="/public/complaints"
            className="text-sm font-medium text-[#64748B] hover:text-[#2563EB] transition-colors"
          >
            Layanan Pengaduan
          </Link>
          <Link
            href="/auth/login"
            className="rounded-lg bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#2563EB]/90 transition-colors"
          >
            Masuk
          </Link>
        </nav>
      </div>
    </header>
  );
}
