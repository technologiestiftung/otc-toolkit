import meow from "meow";
import fs from "fs";
import path from "path";
import { main } from ".";

const cli = meow(
  `
  USAGE:

  ${process.argv[0]} --outdir ./path/to/your/output/folder

  Flags:

    --outdir -o <./relative/path/to/your/output/folder> Optional argument. If not provided it uses the CWD
  `,
  {
    flags: {
      outdir: {
        alias: "o",
        type: "string",
      },
    },
  }
);

if (cli.flags.outdir) {
  if (!fs.existsSync(path.resolve(cli.flags.outdir))) {
    console.error(`path ${cli.flags.outdir} does not exsist`);
    process.exit(1);
  } else {
    if (
      !fs.lstatSync(path.resolve(process.cwd(), cli.flags.outdir)).isDirectory()
    ) {
      console.error(`path ${cli.flags.outdir} is not a directory`);
      process.exit(1);
    }
  }
}
main(cli.flags.outdir).catch((err: Error) => {
  throw err;
});
