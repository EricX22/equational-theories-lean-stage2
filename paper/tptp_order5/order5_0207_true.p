% order5_0207  eq1=31984 eq2=61180  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(X,f(f(Y,f(Y,Y)),Y)),X) )).
fof(goal, conjecture, ! [X,Y] : ( f(f(X,Y),Y) = f(f(X,f(X,Y)),X) )).
