import YAML from "yaml";
import fs from "fs";
import path from "path";
import { YAMLSeq } from "yaml/types";

async function readFile(filePath: string): Promise<string> {
  try {
    if (!fs.existsSync(filePath)) {
      throw new Error("File does not exist");
    }
    const content = fs.readFileSync(filePath, "utf8");
    return content;
  } catch (error) {
    return error;
  }
}

async function writeFile(filePath: string, content: string): Promise<void> {
  fs.writeFileSync(filePath, content);
}
export async function main(outdir?: string): Promise<void> {
  if (!outdir) {
    outdir = process.cwd();
  }
  try {
    const volumesStr = await readFile(
      path.resolve(__dirname, "../templates/res.yml")
    );
    const dcoTemplateStr = await readFile(
      path.resolve(__dirname, "../templates/docker-compose-template.yml")
    );
    const yamlVolumes = YAML.parseDocument(volumesStr);
    const yamlDco = YAML.parseDocument(dcoTemplateStr);
    const volumes: YAMLSeq = yamlVolumes.getIn(["volumes"]);
    // console.log(volumes);
    // process.exit();
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    volumes.items.forEach((item: any) => {
      item.comment = "!Auto genereated. Don't change this";
      // console.log(item);
      yamlDco.addIn(["services", "opendatacam", "volumes"], item);
    });
    // eslint-disable-next-line @typescript-eslint/ban-ts-ignore
    // @ts-ignore
    // const seq = yamlDco.contents.items[0].value;
    // console.log(seq);
    // console.log(yamlDco.toString());
    // console.log();
    await writeFile(
      path.resolve(outdir, "./docker-compose.yml"),
      yamlDco.toString()
    );
    yamlDco.deleteIn(["services", "opendatacam", "volumes"]);
    await writeFile(
      path.resolve(outdir, "./docker-compose.overrides.yml"),
      yamlDco.toString()
    );
  } catch (err) {
    console.error(err);
    // throw err;
  }
}

if (require.main === module) {
  main().catch((err) => {
    throw err;
  });
}
