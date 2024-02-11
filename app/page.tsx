"use client";
import Image from "next/image";
import TextBox from "./components/query";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-left justify-between font-mono text-sm lg:flex flex-col">
        <div className="text-2xl font-bold">End-to-End Deployed Model</div>
        <div>Type your request below: </div>
        <div className="w-full lg:w-1/2">
          <TextBox />
          </div>
      </div>
    </main>
  );
}
