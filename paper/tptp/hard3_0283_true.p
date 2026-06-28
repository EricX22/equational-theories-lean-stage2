% hard3_0283  eq1=2678 eq2=2039  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(Y,Z)),W) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,X),X),f(Y,Z)) )).
