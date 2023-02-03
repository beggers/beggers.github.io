export async function recentPosts(allPosts) {
  allPosts = allPosts.sort((a, b) => {
    return new Date(b.frontmatter.pubDate) - new Date(a.frontmatter.added);
  });
  return allPosts.slice(0, 8);
}

