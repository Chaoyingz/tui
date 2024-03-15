import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import { ComponentProps } from "@/types";

import { Avatar } from "@/components/flect/avatar";
import { Button } from "@/components/flect/button";
import { Container } from "@/components/flect/container";
import { Heading } from "@/components/flect/heading";
import { Link } from "@/components/flect/link";
import { Text } from "@/components/flect/text";
import { Table } from "@/components/flect/table";
import { Outlet } from "@/components/flect/outlet";
import { Form } from "@/components/flect/form";
import { NavLink } from "@/components/flect/nav-link";
import { Paragraph } from "@/components/flect/paragraph";
import { Markdown } from "@/components/flect/markdown";
import { CopyButton } from "@/components/flect/copy-button";
import { CodeBlock } from "@/components/flect/code-block";
import { Custom } from "@/components/flect/custom";

interface ComponentResolver {
  (props: ComponentProps): JSX.Element | null;
  package?: string;
}

interface ResolverContextState {
  resolvers: { [resolverName: string]: ComponentResolver };
  registerResolver: (resolver: ComponentResolver) => void;
}

const ResolverContext = createContext<ResolverContextState | undefined>(
  undefined,
);

export const ResolverProvider: React.FC<{
  children: ReactNode;
  resolver: ComponentResolver;
}> = ({ children, resolver }) => {
  const [resolvers, setResolvers] = useState<{
    [resolverName: string]: ComponentResolver;
  }>({});

  const registerResolver = (resolver: ComponentResolver) => {
    const resolverName = resolver.package;
    if (!resolverName) {
      console.warn(
        "Resolver function is anonymous and cannot be registered. Please provide a named function.",
      );
      return;
    }
    setResolvers((prevResolvers) => ({
      ...prevResolvers,
      [resolverName]: resolver,
    }));
  };

  useEffect(() => {
    registerResolver(resolver);
  }, [resolver]);

  return (
    <ResolverContext.Provider value={{ resolvers, registerResolver }}>
      {children}
    </ResolverContext.Provider>
  );
};

export function ComponentResolver(props: ComponentProps): JSX.Element {
  const context = useContext(ResolverContext);
  if (!context) {
    return <>Component resolver context not found.</>;
  }

  const { resolvers } = context;
  const resolver = resolvers[props.package];
  console.log(props);
  console.log(resolver);
  if (resolver) {
    const resolvedComponent = resolver(props);
    if (resolvedComponent === null) {
      return <>Component of type {props.type} could not be resolved.</>;
    }
    return resolvedComponent;
  }

  return <>No component resolver found for type {props.type}.</>;
}

export const FlectComponentResolver: ComponentResolver = (
  props: ComponentProps,
) => {
  console.log(props);
  switch (props.type) {
    case "avatar":
      return <Avatar {...props} />;
    case "button":
      return <Button {...props} />;
    case "code-block":
      return <CodeBlock {...props} />;
    case "container":
      return <Container {...props} />;
    case "copy-button":
      return <CopyButton {...props} />;
    case "custom":
      return <Custom {...props} />;
    case "form":
      return <Form {...props} />;
    case "heading":
      return <Heading {...props} />;
    case "link":
      return <Link {...props} />;
    case "markdown":
      return <Markdown {...props} />;
    case "nav-link":
      return <NavLink {...props} />;
    case "outlet":
      return <Outlet {...props} />;
    case "paragraph":
      return <Paragraph {...props} />;
    case "table":
      return <Table {...props} />;
    case "text":
      return <Text {...props} />;
    default:
      return null;
  }
};
FlectComponentResolver.package = "flect";
