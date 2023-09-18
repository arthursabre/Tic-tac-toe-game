import sys
sys.path.append("..")
import qlearning as ql
import unittest




class TestAgent(unittest.TestCase): 


    def testcouplevalue(self):
        agent=ql.Agent(ql.TicTacToe)
        state='---------'
        state2='-O-------'
        move=5
        agent.q_value[(state2,move)]=5
        returned_value=agent.couple_value(state,move)
        return_value=agent.couple_value(state2,move)
        self.assertEquals(0.0,returned_value)
        self.assertEquals(5,return_value)
        
    def test_choose_move(self):
        agent=ql.Agent(ql.TicTacToe)
        couple_values={('---------',1):0.3,('---------',2):0.2,('---------',3):0.4 }
        returned_value=agent.choose_move(couple_values,True)
        return_value=agent.choose_move(couple_values,False)
        self.assertEquals(3,returned_value)
        self.assertEquals(2,return_value)
    
    def test_learn_from_move(self):

        agent=ql.Agent(ql.TicTacToe)
        agent.epsilon=1
        game=ql.TicTacToe()
        game.board=['X','X','-','O','-','-','-','-','-']
        state=agent.form_state(game.board)
        expected_value=agent.alpha
        move=agent.learn_from_move(game,2)
        returned_value=agent.q_value[(state,2)]
        self.assertEquals(expected_value,returned_value)
        self.assertEquals(None,move)
        
        second_agent=ql.Agent(ql.TicTacToe)
        second_agent.epsilon=1
        second_game=ql.TicTacToe()
        second_game.board=['O','O','-','X','-','-','-','-','-']
        second_game.player='O'
        state=second_agent.form_state(second_game.board)
        expected_value=-second_agent.alpha
        second_move=second_agent.learn_from_move(second_game,2)
        return_value=second_agent.q_value[(state,2)]
        self.assertEquals(expected_value,return_value)
        self.assertEquals(None,second_move)
        


if __name__ == '__main__':
    unittest.main()
