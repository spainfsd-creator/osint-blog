import React from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import {
  PageMetadata,
  HtmlClassNameProvider,
  ThemeClassNames,
} from '@docusaurus/theme-common';
import BlogLayout from '@theme/BlogLayout';
import BlogListPaginator from '@theme/BlogListPaginator';
import SearchMetadata from '@theme/SearchMetadata';
import BlogPostItems from '@theme/BlogPostItems';
import BlogListPageStructuredData from '@theme/BlogListPage/StructuredData';
import styles from './styles.module.css';

function HeroBanner() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <div className={styles.hero}>
      <div className={styles.heroInner}>
        <div className={styles.heroLogo}>
          <svg
            width="80"
            height="80"
            viewBox="0 0 40 40"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              cx="17"
              cy="17"
              r="12"
              stroke="currentColor"
              strokeWidth="2.5"
              fill="none"
            />
            <line
              x1="26"
              y1="26"
              x2="36"
              y2="36"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
            <circle cx="17" cy="17" r="2.2" fill="currentColor" />
            <circle cx="17" cy="9.5" r="1.6" fill="currentColor" />
            <circle cx="10.5" cy="22" r="1.6" fill="currentColor" />
            <circle cx="23.5" cy="22" r="1.6" fill="currentColor" />
            <line
              x1="17"
              y1="14.8"
              x2="17"
              y2="11.1"
              stroke="currentColor"
              strokeWidth="1.2"
              strokeLinecap="round"
              opacity="0.6"
            />
            <line
              x1="15.2"
              y1="18.8"
              x2="12"
              y2="20.8"
              stroke="currentColor"
              strokeWidth="1.2"
              strokeLinecap="round"
              opacity="0.6"
            />
            <line
              x1="18.8"
              y1="18.8"
              x2="22"
              y2="20.8"
              stroke="currentColor"
              strokeWidth="1.2"
              strokeLinecap="round"
              opacity="0.6"
            />
            <line
              x1="17"
              y1="9.5"
              x2="10.5"
              y2="22"
              stroke="currentColor"
              strokeWidth="0.8"
              strokeLinecap="round"
              opacity="0.3"
            />
            <line
              x1="17"
              y1="9.5"
              x2="23.5"
              y2="22"
              stroke="currentColor"
              strokeWidth="0.8"
              strokeLinecap="round"
              opacity="0.3"
            />
            <line
              x1="10.5"
              y1="22"
              x2="23.5"
              y2="22"
              stroke="currentColor"
              strokeWidth="0.8"
              strokeLinecap="round"
              opacity="0.3"
            />
          </svg>
        </div>
        <h1 className={styles.heroTitle}>{siteConfig.title}</h1>
        <p className={styles.heroTagline}>{siteConfig.tagline}</p>
      </div>
    </div>
  );
}

function BlogListPageMetadata(props: {metadata: any}) {
  const {metadata} = props;
  const {
    siteConfig: {title: siteTitle},
  } = useDocusaurusContext();
  const {blogDescription, blogTitle, permalink} = metadata;
  const isBlogOnlyMode = permalink === '/';
  const title = isBlogOnlyMode ? siteTitle : blogTitle;
  return (
    <>
      <PageMetadata title={title} description={blogDescription} />
      <SearchMetadata tag="blog_posts_list" />
    </>
  );
}

function BlogListPageContent(props: {metadata: any; items: any; sidebar: any}) {
  const {metadata, items, sidebar} = props;
  const isFirstPage = metadata.page === 1;
  return (
    <>
      {isFirstPage && <HeroBanner />}
      <BlogLayout sidebar={sidebar}>
        <BlogPostItems items={items} />
        <BlogListPaginator metadata={metadata} />
      </BlogLayout>
    </>
  );
}

export default function BlogListPage(props: any) {
  return (
    <HtmlClassNameProvider
      className={clsx(
        ThemeClassNames.wrapper.blogPages,
        ThemeClassNames.page.blogListPage,
      )}>
      <BlogListPageMetadata {...props} />
      <BlogListPageStructuredData {...props} />
      <BlogListPageContent {...props} />
    </HtmlClassNameProvider>
  );
}
