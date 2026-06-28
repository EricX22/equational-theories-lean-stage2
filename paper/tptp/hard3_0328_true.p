% hard3_0328  eq1=3069 eq2=153  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(f(X,Y),X),Y),Y) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,X),f(Y,X)) )).
