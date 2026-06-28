% hard3_0234  eq1=2126 eq2=124  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Y),X),f(X,Z)) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(Y,f(f(Y,X),X)) )).
