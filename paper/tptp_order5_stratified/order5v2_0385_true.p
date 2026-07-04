% order5v2_0385  eq1=31425 eq2=18317  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(f(Y,Y),f(Z,Z))),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,Y),f(Z,f(f(Z,Y),Y))) )).
