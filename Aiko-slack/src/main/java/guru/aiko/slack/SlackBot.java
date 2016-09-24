package guru.aiko.slack;

import me.ramswaroop.jbot.core.slack.Bot;
import me.ramswaroop.jbot.core.slack.Controller;
import me.ramswaroop.jbot.core.slack.EventType;
import me.ramswaroop.jbot.core.slack.models.Event;
import me.ramswaroop.jbot.core.slack.models.Message;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.WebSocketSession;

import java.util.regex.Matcher;

/**
 * This Slack bot extends {@link Bot} created by ramswaroop 1.0.0, 05/06/2016
 *
 * @author ukilucas
 * @version 1, September 24, 2016
 */
@Component
public class SlackBot extends Bot {

    private static final Logger logger = LoggerFactory.getLogger(SlackBot.class);

    /**
     * This tocken is SPECIFIC to you Slack bot application, you have to generate it yourself at
     * <a href="https://my.slack.com/services/new/bot">creating a new bot</a>
     * and place it in resources/application.properties text file.
     * slackBotToken=XYZ
     */
    @Value("${slackBotToken}")
    private String slackToken;

    @Override
    public String getSlackToken() {
        if (slackToken == null || slackToken.length() == 0) {
            System.err.println("Missing slackBotToken entry in resources/application.properties visit https://my.slack.com/services/new/bot");
        }
        return slackToken;
    }

    private String botName;
    private String eventType;

    @Override
    public Bot getSlackBot() {
        return this;
    }

    /**
     * Invoked when the bot receives a direct mention (@Aiko: message)
     * or message in a direct chat.
     * Expectation is that Aiko will respond to message when addressed directly.
     *
     * @param session
     * @param event
     */
    @Controller(events = {EventType.DIRECT_MENTION, EventType.DIRECT_MESSAGE})
    public void onReceiveDM(WebSocketSession session, Event event) {
        logger.debug("Channel " + event.getChannel());
        logger.debug("Comment " + event.getComment());
        logger.debug("User " + event.getItemUser());

        eventType = event.getType();
        log("Event Tyep: " + eventType);

        botName = capitalizeName(slackService.getCurrentUser().getName());
        String eventText = event.getText();

        StringBuffer sb = new StringBuffer();

        if (eventType.equals(EventType.DIRECT_MESSAGE.name()))
            sb.append("I am responding because you adderesd me in a direct chat" + "\n");
        sb.append("Hi, I am " + botName + "\n");
        sb.append("received text " + eventText + "\n");
        //    sb.append("Channel " + event.getChannel() + "\n");
        //    sb.append("Item " + event.getItem() + "\n");
        //    sb.append("Latest " + event.getLatest() + "\n");
        //    sb.append("Comment " + event.getComment() + "\n");
        //    sb.append("User " + event.getItemUser() + "\n");
        //    sb.append("Deleted Ts " + event.getDeletedTs() + "\n");
        //    sb.append("domain " + event.getDomain() + "\n");
        //    sb.append("presence " + event.getPresence() + "\n");
        //    sb.append("type " + event.getType() + "\n");
        //    sb.append("user id " + event.getUserId() + "\n");
        //    sb.append("names " + event.getNames() + "\n");
        //    sb.append("channel id " + event.getChannelId() + "\n");
        //    sb.append("replay to " + event.getReplyTo() + "\n");

        reply(session, event, new Message(sb.toString()));
    }

    private void log(String text) {
        System.err.println(text);
    }

    /**
     * Invoked when bot receives an event of type message with text satisfying the pattern {@code
     * ([a-z ]{2})(\d+)([a-z ]{2})}. For example, messages like "ab12xy" or "ab2bc" etc will invoke
     * this method.
     *
     * @param session
     * @param event
     */
    @Controller(
            events = {EventType.MESSAGE, EventType.DIRECT_MESSAGE},
            pattern = "^([a-z ]{2})(\\d+)([a-z ]{2})$"
    )
    public void onReceiveMessage(WebSocketSession session, Event event, Matcher matcher) {

        String botName = capitalizeName(slackService.getCurrentUser().getName());
        String eventText = event.getText();

        StringBuffer sb = new StringBuffer();
        sb.append("Hi, I am " + botName + "\n");
        sb.append("received text " + eventText + "\n");

        sb.append("First group: " + matcher.group(0) + "\n");
        sb.append("Second group: " + matcher.group(1) + "\n");
        sb.append("Third group: " + matcher.group(2) + "\n");
        sb.append("Fourth group: " + matcher.group(3) + "\n");

        reply(session, event, new Message(sb.toString()));
    }

    /**
     * Invoked when an item is pinned in the channel.
     *
     * @param session
     * @param event
     */
    @Controller(events = EventType.PIN_ADDED)
    public void onPinAdded(WebSocketSession session, Event event) {
        reply(
                session,
                event,
                new Message("Thanks for the pin! You can find all pinned items under channel details."));
    }

    /**
     * Invoked when bot receives an event of type file shared. NOTE: You can't reply to this event as
     * slack doesn't send a channel id for this event type. You can learn more about <a
     * href="https://api.slack.com/events/file_shared">file_shared</a> event from Slack's Api
     * documentation.
     *
     * @param session
     * @param event
     */
    @Controller(events = EventType.FILE_SHARED)
    public void onFileShared(WebSocketSession session, Event event) {
        logger.info("File shared: {}", event);
    }

    /**
     * Conversation feature of JBot. This method is the starting point of the conversation (as it
     * calls {@link Bot#startConversation(Event, String)} within it. You can chain methods which will
     * be invoked one after the other leading to a conversation. You can chain methods with {@link
     * Controller#next()} by specifying the method name to chain with.
     *
     * @param session
     * @param event
     */
    @Controller(
            events = {EventType.MESSAGE, EventType.DIRECT_MESSAGE},
            pattern = "(setup meeting)",
            next = "confirmTiming"
    )
    public void setupMeeting(WebSocketSession session, Event event) {
        startConversation(event, "confirmTiming"); // start conversation
        reply(session, event, new Message("At what time? (ex. 15:30)"));
    }

    /**
     * This method is chained with {@link SlackBot#setupMeeting(WebSocketSession, Event)}.
     */
    @Controller(next = "askTimeForMeeting")
    public void confirmTiming(WebSocketSession session, Event event) {
        reply(
                session,
                event,
                new Message(
                        "Your meeting is set at "
                                + event.getText()
                                + ". Would you like to repeat it tomorrow?"));
        nextConversation(event); // jump to next question in conversation
    }

    /**
     * This method is chained with {@link SlackBot#confirmTiming(WebSocketSession, Event)}.
     *
     * @param session
     * @param event
     */
    @Controller(next = "askWhetherToRepeat")
    public void askTimeForMeeting(WebSocketSession session, Event event) {
        if (event.getText().contains("yes")) {
            reply(session, event, new Message("Okay. Would you like me to set a reminder for you?"));
            nextConversation(event); // jump to next question in conversation
        } else {
            reply(
                    session,
                    event,
                    new Message("No problem. You can always schedule one with 'setup meeting' command."));
            stopConversation(event); // stop conversation only if user says no
        }
    }

    /**
     * This method is chained with {@link SlackBot#askTimeForMeeting(WebSocketSession, Event)}.
     *
     * @param session
     * @param event
     */
    @Controller
    public void askWhetherToRepeat(WebSocketSession session, Event event) {
        if (event.getText().contains("yes")) {
            reply(session, event, new Message("OK, I will remind you tomorrow before the meeting."));
        } else {
            reply(session, event, new Message("OK, just today."));
        }
        stopConversation(event); // stop conversation
    }

    public String capitalizeName(String name) {
        StringBuilder word = new StringBuilder();
        word.append(name);
        word.setCharAt(0, Character.toUpperCase(word.charAt(0)));
        return word.toString();
    }
}
