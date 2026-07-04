% order5_0047  eq1=6039 eq2=46168  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(Y,f(Z,f(f(Z,Y),Y)))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(X,Y),f(Y,f(Y,Y))) )).
