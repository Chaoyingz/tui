import { AnyComponents } from "@/components/flect/any-component";
import { ComponentProps } from "@/types";

export interface ContainerProps {
  type: "container";
  className?: string;
  children?: ComponentProps[];
  tag: "div" | "section" | "header" | "footer" | "main" | "nav" | "aside";
}

export function Container(props: ContainerProps) {
  const { children, className, tag } = props;
  const Tag = tag || "div";
  return (
    <Tag className={className}>
      <AnyComponents children={children} />
    </Tag>
  );
}
