% hard3_0377  eq1=3798 eq2=399  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,X),f(W,Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Z,Y),Y) )).
