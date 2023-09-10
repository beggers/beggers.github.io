This is my personal website.

It is, uh, not a showcase of my ability to write clean and maintainable code. Enter at your own risk.

I thought it would be fun to make this SSR -- wow, what if the page just had HTML? -- but failed
to acount for the performance cost that would incur. I moved from render.com to AWS lambda because
Render's free tier took 30+ seconds to cold boot an instance for my site. But in reality, the whole thing
should just be a static blob served by S3. Maybe someday!