import { SITE_TITLE } from '../config';

export function pageTitle(pageTitle) {
  if (pageTitle == null) {
    return SITE_TITLE;
  }
  return pageTitle.concat(": ").concat(SITE_TITLE);
}
