% hard3_0258  eq1=2451 eq2=2240  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(f(X,Y),Y)),Z) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(f(X,f(X,f(X,Y))),X) )).
