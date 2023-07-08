import { POSTS_ON_FRONT_PAGE } from '../config.ts';

export function filterAndSort(posts) {
  posts = posts.filter((p) => {
    return p.frontmatter.publish;
  });
  posts = posts.sort((a, b) => {
    return (
      new Date(b.frontmatter.published) - new Date(a.frontmatter.published)
    );
  });
  return posts;
}

export async function recentPosts(allPosts) {
  allPosts = filterAndSort(allPosts);
  return allPosts.slice(0, POSTS_ON_FRONT_PAGE);
}

export function getTagsToPosts(allPosts) {
  allPosts = filterAndSort(allPosts);
  var d = {};
  allPosts.forEach((post) => {
    const tags = post.frontmatter.tags;
    if (!tags) {
      return;
    }
    tags.forEach((tag) => {
      if (!d[tag]) {
        d[tag] = [];
      }
      d[tag].push(post);
    });
  });
  return d;
}
