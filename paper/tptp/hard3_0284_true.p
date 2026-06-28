% hard3_0284  eq1=2678 eq2=3462  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),f(Y,Z)),W) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,X) = f(X,f(f(Y,X),Y)) )).
