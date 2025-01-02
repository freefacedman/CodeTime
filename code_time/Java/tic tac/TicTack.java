import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class TicTacToe extends JFrame implements ActionListener {
    private JButton[] buttons = new JButton[9];
    private int currentPlayer; // 0 for X, 1 for O
    private int moveCount;

    public TicTacToe() {
        setTitle("Tic-Tac-Toe");
        setSize(400, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        initializeGUI();
        currentPlayer = 0; // X starts
        moveCount = 0;
    }

    private void initializeGUI() {
        setLayout(new GridLayout(3, 3));
        
        Font font = new Font("Arial", Font.BOLD, 60);
        
        for (int i = 0; i < 9; i++) {
            buttons[i] = new JButton("");
            buttons[i].setFont(font);
            buttons[i].setFocusPainted(false);
            buttons[i].addActionListener(this);
            add(buttons[i]);
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        JButton clickedButton = (JButton) e.getSource();

        if (!clickedButton.getText().equals("")) {
            // Button already clicked
            return;
        }

        if (currentPlayer == 0) {
            clickedButton.setText("X");
        } else {
            clickedButton.setText("O");
        }

        moveCount++;

        if (checkForWin()) {
            String winner = currentPlayer == 0 ? "X" : "O";
            JOptionPane.showMessageDialog(this, "Player " + winner + " wins!", "Game Over", JOptionPane.INFORMATION_MESSAGE);
            resetGame();
            return;
        }

        if (moveCount == 9) {
            JOptionPane.showMessageDialog(this, "It's a draw!", "Game Over", JOptionPane.INFORMATION_MESSAGE);
            resetGame();
            return;
        }

        // Switch player
        currentPlayer = 1 - currentPlayer;
    }

    private boolean checkForWin() {
        int[][] winPatterns = {
            {0, 1, 2},
            {3, 4, 5},
            {6, 7, 8},
            {0, 3, 6},
            {1, 4, 7},
            {2, 5, 8},
            {0, 4, 8},
            {2, 4, 6}
        };

        String currentMark = currentPlayer == 0 ? "X" : "O";

        for (int[] pattern : winPatterns) {
            if (buttons[pattern[0]].getText().equals(currentMark) &&
                buttons[pattern[1]].getText().equals(currentMark) &&
                buttons[pattern[2]].getText().equals(currentMark)) {
                return true;
            }
        }

        return false;
    }

    private void resetGame() {
        for (JButton button : buttons) {
            button.setText("");
        }
        currentPlayer = 0;
        moveCount = 0;
    }

    public static void main(String[] args) {
        // Ensure the GUI is created on the Event Dispatch Thread
        SwingUtilities.invokeLater(() -> {
            TicTacToe game = new TicTacToe();
            game.setVisible(true);
        });
    }
}
