import POSTS_ON_FRONT_PAGE from '../config.ts';

export async function recentPosts(allPosts) {
  allPosts = allPosts.filter((p) => {
    return p.frontmatter.publish;
  });
  allPosts = allPosts.sort((a, b) => {
    return new Date(b.frontmatter.published) - new Date(a.frontmatter.published);
  });
  return allPosts.slice(0, POSTS_ON_FRONT_PAGE);
}

export function getTagsToPosts(allPosts) {
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
