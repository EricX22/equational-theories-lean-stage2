% order5v2_0750  eq1=18221 eq2=30389  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Y),f(X,f(f(Y,Z),Y))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(X,f(f(Y,Z),X))),Y) )).
