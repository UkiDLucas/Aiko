package guru.aiko;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * @author ukilucas September 24, 2016
 */
@SpringBootApplication(scanBasePackages = {"me.ramswaroop.jbot", "guru.aiko"})
public class AikoSlackApplication {

    /**
     * You can run this class directly from IDE,
     * or from command line.
     * Review README.md file for setup instructions.
     *
     * @param args - no arguments at this time
     */
    public static void main(String[] args) {

        SpringApplication.run(AikoSlackApplication.class, args);
    }
}
