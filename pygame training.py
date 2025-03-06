import sys, pygame
import random

pygame.init()

my_font = pygame.font.Font(None, 62)
instructions_text = my_font.render("Press the key matching the ink colour:", 1, (255, 255, 255))
instructions_text_pos = instructions_text.get_rect(center=(400, 200))

instructions_text2 = my_font.render("B for Blue, R for Red, G for Green", 1, (255, 255, 255))
instructions_text_pos2 = instructions_text.get_rect(center=(400, 300))

start_text = my_font.render("Press any key to start", 1, (255, 255, 255))
start_text_pos = start_text.get_rect(center=(400, 400))

clrs = [(0, 0, 255), (225, 0, 0), (0, 255, 0)] 
actv_clr = 0
rslts = {'trial_num': 0, 'colour': None, 'time': None, 'feedback': None}

# pygame
mywindow = pygame.display.set_mode([800, 800])
running = True
myrt_clock = pygame.time.Clock()

trl = 0  # Trial number starts from 0
trial_type = 'circle'  # Start with circle trials
trial_count = 1
max_trials = 60  # Total trials
start_screen = True

# Feedback
feedback_time = 0
is_feedback = False

# Incongruent colour set up
def get_incongruent_ink_colour(word_colour):
    possible_colours = [0, 1, 2] 
    possible_colours.remove(word_colour)
    return random.choice(possible_colours)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Start screen accept any key press to continue
        if start_screen and event.type == pygame.KEYDOWN:
            start_screen = False
            t1 = pygame.time.get_ticks()
            continue

        # Check key press when not on feedback screen
        if event.type == pygame.KEYDOWN and not is_feedback and not start_screen:
            colour_map = {pygame.K_b: 0, pygame.K_r: 1, pygame.K_g: 2}
            
            if event.key in colour_map:
                user_input = ['Blue', 'Red', 'Green'][colour_map[event.key]]
                input_colour = colour_map[event.key]
                
                # Does input match the ink colour?
                if (trial_type == 'circle' and input_colour == actv_clr) or (trial_type == 'congruent' and input_colour == actv_clr) or (trial_type == 'incongruent' and input_colour == actv_clr):
                    rslts['feedback'] = "Correct"
                else:
                    rslts['feedback'] = "Incorrect"
                
                # Response time
                t2 = pygame.time.get_ticks()
                rslts['time'] = (t2 - t1) / 1000
                rslts['trial_num'] = rslts['trial_num'] + 1
                print(rslts)
                t1 = t2

                # Feedback
                is_feedback = True
                feedback_time = pygame.time.get_ticks()

                trial_count += 1

    # Feedback
    if is_feedback:
        feedback_text = my_font.render(rslts['feedback'], 1, (255, 255, 255))
        feedback_pos = feedback_text.get_rect(center=(400, 400))
        
        mywindow.fill((0, 0, 0))
        
        mywindow.blit(feedback_text, feedback_pos)
        
        if pygame.time.get_ticks() - feedback_time > 1000:
            is_feedback = False

            # Next trial
            if trial_count <= 20:
                actv_clr = random.choice([0, 1, 2])
                trial_type = 'circle'
                t1 = pygame.time.get_ticks()
            elif trial_count <= 40:
                actv_clr = random.choice([0, 1, 2])
                trial_type = 'congruent'
                t1 = pygame.time.get_ticks()
            elif trial_count <= 60:
                word_colour = random.choice([0, 1, 2])
                ink_colour = get_incongruent_ink_colour(word_colour)
                actv_clr = ink_colour 
                
                trial_type = 'incongruent'
                t1 = pygame.time.get_ticks() 
            else:
                print("Trial limit reached.")
                running = False

    # Trial
    if not is_feedback:
        mywindow.fill((0, 0, 0))
        
        # Start screen
        if start_screen:
            mywindow.blit(start_text, start_text_pos)
            mywindow.blit(instructions_text, instructions_text_pos)
            mywindow.blit(instructions_text2, instructions_text_pos2)
        else:
            if trial_type == 'circle':
                pygame.draw.circle(mywindow, clrs[actv_clr], (400, 400), 200)
            
            elif trial_type == 'congruent':
                active_text = my_font.render(f"{['Blue', 'Red', 'Green'][actv_clr]}", 1, clrs[actv_clr])
                active_text_pos = active_text.get_rect(center=(400, 400))
                mywindow.blit(active_text, active_text_pos)
            
            elif trial_type == 'incongruent':
                word = ['Blue', 'Red', 'Green'][word_colour] 
                active_text = my_font.render(word, 1, clrs[actv_clr])
                active_text_pos = active_text.get_rect(center=(400, 400))
                mywindow.blit(active_text, active_text_pos)

    pygame.display.flip()

pygame.quit()
sys.exit()