% hard3_0220  eq1=2069 eq2=1635  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,Y),Y),f(Z,W)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,X),f(f(Y,X),Y)) )).
