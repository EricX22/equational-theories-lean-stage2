% hard3_0292  eq1=2757 eq2=835  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Y),f(Z,Y)),X) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(Y,X),f(Y,X))) )).
