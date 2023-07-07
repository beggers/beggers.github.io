import { getTagsToPosts } from './posts';

export function getTagsToCounts(allPosts) {
    var tagsToPosts = getTagsToPosts(allPosts);
    var d = {};
    Object.keys(tagsToPosts).forEach((tag) => {
        d[tag] = tagsToPosts[tag].length;
    });
    return d;
}
