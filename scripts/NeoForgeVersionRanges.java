import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import org.apache.maven.artifact.versioning.DefaultArtifactVersion;
import org.apache.maven.artifact.versioning.VersionRange;

class NeoForgeVersionRanges {
    public static void main(String[] args) throws Exception {
        var input = new BufferedReader(new InputStreamReader(System.in, StandardCharsets.UTF_8));
        for (String line; (line = input.readLine()) != null; ) {
            var fields = line.split("\t", -1);
            var range = VersionRange.createFromVersionSpec(fields[0]);
            var target = fields[1];
            var version = fields[2];
            boolean matches = version.equals("0.0NONE") || range.containsVersion(new DefaultArtifactVersion(version));
            // FML 4.0.45 VersionSupportMatrix for Minecraft 1.21.1.
            if (!matches && args[0].equals("1.21.1")) {
                var alias = switch (target) {
                    case "minecraft" -> "1.21";
                    case "neoforge" -> "21.0.166";
                    default -> null;
                };
                matches = alias != null && range.containsVersion(new DefaultArtifactVersion(alias));
            }
            System.out.println(matches ? "yes" : "no");
        }
    }
}
