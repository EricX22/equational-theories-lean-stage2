% hard3_0287  eq1=2683 eq2=3715  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,Y),f(Z,Y)),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(X,X),f(Y,Y)) )).
