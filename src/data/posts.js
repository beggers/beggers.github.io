export async function recentPosts(allPosts) {
  allPosts = allPosts.sort((a, b) => {
    return new Date(b.frontmatter.published) - new Date(a.frontmatter.published);
  });
  return allPosts.slice(0, 8);
}

