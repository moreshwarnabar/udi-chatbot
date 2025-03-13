export interface Message {
  role: 'system' | 'user';
  content: string;
}

export interface BulletPoint {
  text: string;
  subpoints: BulletPoint[];
}

interface ContentBlock {
  content: string | BulletPoint[];
}

export interface Reply {
  response: ContentBlock[];
}
