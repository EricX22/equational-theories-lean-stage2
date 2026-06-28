% hard3_0197  eq1=1806 eq2=3316  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,Z),f(f(W,X),X)) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(X,f(Y,f(X,Y))) )).
