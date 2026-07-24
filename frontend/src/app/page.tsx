import { PublicHeader } from "@/components/layouts/public-header";
import { PublicFooter } from "@/components/layouts/public-footer";
import { HomeHero } from "@/components/features/public/home-hero";
import { AboutVision } from "@/components/features/public/about-vision";
import { AboutMission } from "@/components/features/public/about-mission";
import { HowItWorks } from "@/components/features/public/how-it-works";
import { ChatBubble } from "@/components/features/public/chat-bubble";

export default function HomePage() {
  return (
    <>
      <PublicHeader />
      <main className="flex-1">
        <HomeHero />
        <AboutVision />
        <AboutMission />
        <HowItWorks />
      </main>
      <PublicFooter />
      <ChatBubble />
    </>
  );
}
