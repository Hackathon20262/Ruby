import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    budget: false,
    teamSize: false,
    timeline: false,
    authority: false,
  });
}