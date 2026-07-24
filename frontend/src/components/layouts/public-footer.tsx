import Link from "next/link";
import Image from "next/image";

export function PublicFooter() {
  return (
    <footer>
      {/* CTA Banner */}
      <div className="bg-[#0D9488] py-14">
        <div className="mx-auto flex max-w-7xl flex-col items-center gap-6 text-center sm:flex-row sm:text-left sm:justify-between px-4 sm:px-6 lg:px-16">
          <div className="max-w-2xl">
            <h2 className="text-2xl font-semibold leading-snug text-white">
              Mau menjadi bagian dari Perubahan? Bersama SIGAP wujudkan generasi sehat dengan pangan yang aman & terverifikasi
            </h2>
          </div>
          <Link
            href="/public/vendors/register"
            className="inline-flex shrink-0 items-center gap-2 rounded-lg bg-white px-6 py-3 text-sm font-semibold text-[#0D9488] hover:bg-teal-50 transition-colors"
          >
            Daftar menjadi Mitra SPPG
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 8H13M13 8L9.5 4.5M13 8L9.5 11.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </Link>
        </div>
      </div>

      {/* Bottom Footer */}
      <div className="bg-[#2563EB] py-6">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 sm:flex-row px-4 sm:px-6 lg:px-16">
          <Image
            src="/assets/images/Logo Dark.png"
            alt="SIGAP"
            width={90}
            height={30}
            className="h-7 w-auto brightness-0 invert"
          />
          <nav className="flex items-center gap-3 text-sm text-white/80">
            <Link href="/kebijakan-privasi" className="hover:text-white transition-colors">
              Kebijakan Privasi
            </Link>
            <span className="text-white/40">|</span>
            <Link href="/syarat-ketentuan" className="hover:text-white transition-colors">
              Syarat dan Ketentuan
            </Link>
            <span className="text-white/40">|</span>
            <Link href="/hubungi-kami" className="hover:text-white transition-colors">
              Hubungi Kami
            </Link>
          </nav>
          <p className="text-sm text-white/60">
            &copy;2026 Copyrights. SIGAP &mdash; Sistem Integrasi Gizi dan Akuntabilitas Pangan
          </p>
        </div>
      </div>
    </footer>
  );
}
