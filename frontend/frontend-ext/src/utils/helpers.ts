import { Reply, BulletPoint } from '../types';

export const formatReply = (reply: Reply) => {
  const message = reply.response
    .map(block =>
      typeof block.content === 'string'
        ? block.content
        : formatBulletPoints(block.content)
    )
    .join('\n');

  return message;
};

const formatBulletPoints = (
  bulletPoints: BulletPoint[],
  indentLevel = 0
): string => {
  const indent = '  '.repeat(indentLevel);

  return bulletPoints
    .map(
      bullet =>
        `${indent}- ${bullet.text}\n${formatBulletPoints(
          bullet.subpoints,
          indentLevel + 1
        )}`
    )
    .join('');
};
